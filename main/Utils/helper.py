
def image_path_name(self, filename):
    ext = filename.split('.')[-1]
    new_title = self.title.replace(" ", "_").lower()
    return f"product_images/{new_title}.{ext}"