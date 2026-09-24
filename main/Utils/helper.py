from datetime import datetime
import uuid

def image_path_name(self, filename):
    ext = filename.split('.')[-1]
    new_name = self.name.replace(" ", "_").lower()
    unique_id = uuid.uuid4().hex[:8]
    return f"product_images/{new_name}/{new_name}{unique_id}.{ext}"