from django.db import models

class LabeledImage(models.Model):
    DATASET_SPLIT_CHOICES = [
        ('train', 'Training Set'),
        ('test', 'Test Set'),
        ('val', 'Validation Set'),
    ]
    
    image = models.ImageField(upload_to='labeled_data/')
    generated_caption = models.TextField(blank=True, null=True)
    user_caption = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    needs_correction = models.BooleanField(default=False)
    dataset_split = models.CharField(
        max_length=10, 
        choices=DATASET_SPLIT_CHOICES,
        default='train'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Thêm trạng thái kiểm duyệt
    verified = models.BooleanField(default=False)
    verified_by = models.CharField(max_length=100, blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Image {self.id} - {self.dataset_split} - Approved: {self.approved}"
    
    @property
    def final_caption(self):
        return self.user_caption if self.user_caption else self.generated_caption
    
    @property
    def is_corrected(self):
        return bool(self.user_caption and self.user_caption != self.generated_caption)

    class Meta:
        ordering = ['-created_at']