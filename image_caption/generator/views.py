# views.py - UPDATED TO MATCH CHAPTER 4 DESCRIPTION
import os
import pickle
import numpy as np
from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

from .models import LabeledImage
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load AI models once at startup (Singleton pattern)
try:
    mobilenet_model = MobileNetV2(weights="imagenet")
    feature_extractor = Model(inputs=mobilenet_model.inputs, 
                            outputs=mobilenet_model.layers[-2].output)
    
    caption_model = load_model(os.path.join(settings.BASE_DIR, "../core/mymodel.h5"))
    
    with open(os.path.join(settings.BASE_DIR, "../core/tokenizer.pkl"), "rb") as f:
        tokenizer = pickle.load(f)
        
    MAX_CAPTION_LENGTH = 34
    MODEL_LOADED = True
except Exception as e:
    print(f"Model loading error: {e}")
    MODEL_LOADED = False

def index(request):
    """
    Main view for image upload and caption generation
    Corresponds to Use Case: 'Tải ảnh lên' và 'Sinh mô tả tự động'
    """
    context = {
        'caption': None,
        'uploaded_file_url': None, 
        'saved_image_id': None,
        'model_loaded': MODEL_LOADED
    }
    
    if request.method == "POST" and MODEL_LOADED:
        # Handle image upload and caption generation
        if "image" in request.FILES:
            try:
                image_file = request.FILES["image"]
                
                # Save uploaded file
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "uploads"))
                filename = fs.save(image_file.name, image_file)
                uploaded_file_url = fs.url(f"uploads/{filename}")
                image_path = os.path.join(settings.MEDIA_ROOT, "uploads", filename)

                # Process image and extract features
                image = load_img(image_path, target_size=(224, 224))
                image = img_to_array(image)
                image = np.expand_dims(image, axis=0)
                image = preprocess_input(image)

                # Generate image features using MobileNetV2
                image_features = feature_extractor.predict(image, verbose=0)
                
                # Generate caption using trained model
                raw_caption = generate_caption(caption_model, image_features, tokenizer, MAX_CAPTION_LENGTH)
                clean_caption = raw_caption.replace("startseq", "").replace("endseq", "").strip()

                # Save to database
                labeled_image = LabeledImage.objects.create(
                    image=f"uploads/{filename}",
                    generated_caption=clean_caption
                )

                context.update({
                    'caption': clean_caption,
                    'uploaded_file_url': uploaded_file_url,
                    'saved_image_id': labeled_image.id
                })
                
            except Exception as e:
                context['error'] = f"Error processing image: {str(e)}"

    return render(request, "generator/index.html", context)

def generate_caption(model, image_features, tokenizer, max_length):
    """
    Generate caption using the trained LSTM model
    Implements the autoregressive sequence generation described in Chapter 3
    """
    caption = "startseq"
    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([caption])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([image_features, sequence], verbose=0)
        predicted_index = np.argmax(yhat)
        predicted_word = get_word_from_index(predicted_index, tokenizer)
        
        if predicted_word is None:
            break
            
        caption += " " + predicted_word
        
        if predicted_word == "endseq":
            break
            
    return caption

def get_word_from_index(index, tokenizer):
    """Helper function to convert index back to word"""
    for word, idx in tokenizer.word_index.items():
        if idx == index:
            return word
    return None

@csrf_exempt
def handle_caption_feedback(request):
    """
    Handle user feedback for captions (approve/correct)
    Corresponds to Use Case: 'Phê duyệt mô tả' và 'Chỉnh sửa mô tả'
    """
    if request.method == "POST":
        image_id = request.POST.get("image_id")
        action = request.POST.get("action")
        
        try:
            labeled_image = LabeledImage.objects.get(id=image_id)
            
            if action == "approve":
                labeled_image.user_caption = labeled_image.generated_caption
                labeled_image.approved = True
                labeled_image.save()
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Caption approved successfully!'
                })
                
            elif action == "correct":
                user_caption = request.POST.get("user_caption")
                dataset_split = request.POST.get("dataset_split", "train")
                
                labeled_image.user_caption = user_caption
                labeled_image.approved = True
                labeled_image.needs_correction = True
                labeled_image.dataset_split = dataset_split
                labeled_image.save()
                
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Caption correction saved!'
                })
                
        except LabeledImage.DoesNotExist:
            return JsonResponse({
                'status': 'error', 
                'message': 'Image not found'
            })
    
    return JsonResponse({
        'status': 'error', 
        'message': 'Invalid request'
    })


def statistics_dashboard(request):
    """
    Statistics and analytics dashboard
    Corresponds to Use Case: 'Xem thống kê'
    """
    
    # ... (Logic thống kê giữ nguyên)
    total_images = LabeledImage.objects.count()
    approved_images = LabeledImage.objects.filter(approved=True).count()
    corrected_images = LabeledImage.objects.filter(needs_correction=True).count()
    approval_rate = (approved_images / total_images * 100) if total_images > 0 else 0
    
    # 1. Lấy tất cả các hoạt động để phân trang
    all_activity = LabeledImage.objects.all().order_by('-created_at')
    
    # 2. Khởi tạo Paginator (ví dụ: 10 mục mỗi trang)
    paginator = Paginator(all_activity, 10) 
    
    # 3. Lấy số trang hiện tại từ request
    page_number = request.GET.get('page')
    
    # 4. Lấy đối tượng trang
    page_obj = paginator.get_page(page_number)
    
    context = {
        'stats': {
            'total_images': total_images,
            'approved_images': approved_images,
            'corrected_images': corrected_images,
            'approval_rate': round(approval_rate, 2),
        },
        'page_obj': page_obj  # Truyền đối tượng trang đã được phân trang
    }
    
    return render(request, "generator/stats.html", context)