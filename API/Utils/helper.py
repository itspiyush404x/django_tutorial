from datetime import datetime
import uuid

def product_image_path_name(self, filename):
    ext = filename.split('.')[-1]
    new_name = self.product.slug
    unique_id = uuid.uuid4().hex[:8]
    return f"product_images/{new_name}/{new_name}-{unique_id}.{ext}"


def brand_logo_path_name(self, filename):
    ext = filename.split('.')[-1]
    new_name = self.slug
    unique_id = uuid.uuid4().hex[:8]
    return f"Brand_logos/{new_name}.{ext}"

