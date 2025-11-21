import os, json, base64
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# ---------------- PATHS ----------------
DATA_PATH = os.path.join(settings.BASE_DIR, 'data', 'ecg_data.json')
FINAL_PATH = os.path.join(settings.BASE_DIR, 'data', 'final_data.json')
PROGRESS_PATH = os.path.join(settings.BASE_DIR, 'data', 'progress.json')
IMG_DIR = os.path.join(settings.MEDIA_ROOT, 'ecg_images')

# ---------------- INDEX VIEW ----------------
def index(request):
    # Get all images
    images = sorted([f for f in os.listdir(IMG_DIR) if f.lower().endswith('.jpg')])

    # Start from last processed image
    start_index = 0
    if os.path.exists(PROGRESS_PATH):
        try:
            with open(PROGRESS_PATH) as f:
                data = json.load(f)
                last_image = data.get('last_image')
                if last_image in images:
                    start_index = images.index(last_image) + 1
        except json.JSONDecodeError:
            start_index = 0

    # Convert current image to base64 for OpenSeadragon
    if images:
        img_path = os.path.join(IMG_DIR, images[start_index])
        with open(img_path, 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')
    else:
        img_base64 = ""

    context = {
        'images': images,
        'start_index': start_index,
        'img_base64': img_base64
    }
    return render(request, 'viewer/index.html', context)

# ---------------- GET JSON DATA ----------------
def get_image_data(request, img_name):
    """Return JSON data for a specific image"""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH) as f:
            data = json.load(f)
        return JsonResponse(data.get(img_name, {}))
    return JsonResponse({})

# ---------------- SAVE VERIFIED DATA ----------------
@csrf_exempt  # dev/testing only
def save_verified_data(request):
    """Save verified data and update progress"""
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            img_name = payload['image_name']
            verified_data = payload['verified_data']

            # Load existing final_data safely
            if os.path.exists(FINAL_PATH):
                try:
                    with open(FINAL_PATH) as f:
                        final_data = json.load(f)
                except json.JSONDecodeError:
                    final_data = {}
            else:
                final_data = {}

            # Update final_data
            final_data[img_name] = verified_data

            # Save final_data
            with open(FINAL_PATH, 'w') as f:
                json.dump(final_data, f, indent=4)

            # Update progress
            with open(PROGRESS_PATH, 'w') as f:
                json.dump({'last_image': img_name}, f)

            # ✅ Send success
            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def next_image_base64(request, img_name):
    img_path = os.path.join(IMG_DIR, img_name)
    if os.path.exists(img_path):
        with open(img_path, 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')
        return JsonResponse({'img_base64': img_base64})
    return JsonResponse({'img_base64': ''})
