# cms_export_fixed.py
import os
import django
import sys, re

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from kutub.models import Manuscript
from django.conf import settings
from django.urls import reverse

# Temporarily add 'testserver' to ALLOWED_HOSTS
original_allowed_hosts = settings.ALLOWED_HOSTS
settings.ALLOWED_HOSTS += ['testserver']

def process_html(html_content):
    # Add custom processing here
    # Find the position of <body> and <div class="themata-body">
    body_start = html_content.find("<body")
    if body_start == -1:
        print(f"  Warning: No <body> tag found")
        body_start = 0
        return html_content
    else:
        # Find the end of the body tag
        body_tag_end = html_content.find(">", body_start)
        if body_tag_end == -1:
            body_tag_end = body_start
            print(f" Warning: malformed html body tag")
            return html_content            
        else:
            body_tag_end += 1  # Include the closing bracket
    
    # Find the themata-body div
    modified_html = None
    themata_body_start = html_content.find('<div class="themata-body"')    
    if themata_body_start == -1:
        print(f"Warning: No div with class 'themata-body' found")
        # Keep the HTML as is
        modified_html = html_content
    else:
        # Remove content between body start and themata-body div
        modified_html = html_content[:body_tag_end] + html_content[themata_body_start:]
        print(f"Removed content before themata-body")
        # Step 2: Remove all divs with class="float-right"
        # This uses regex to handle all variations of the div tag
        float_right_pattern = re.compile(r'<div\s+[^>]*class\s*=\s*["\'](?:[^"\']*\s+)?float-right(?:\s+[^"\']*)?["\'][^>]*>.*?</div>', re.DOTALL)
        modified_html, count = float_right_pattern.subn('', modified_html)
        if count > 0:
            print(f"Removed {count} float-right div(s)")
    
    # Add iframe URL processing
    iframe_pattern = re.compile(r'<iframe\s+[^>]*src=["\']([^"\']+)["\'][^>]*>')
    modified_html = iframe_pattern.sub(f'<iframe src="/manuscripts/iiif/', modified_html)

# Output directory
output_dir = "exported_pages/"
os.makedirs(output_dir, exist_ok=True)

# Get a user with proper permissions
User = get_user_model()
user = User.objects.filter(is_staff=True).first()
if not user:
    print("No user with permissions found!")
    sys.exit(1)

print(f"Using user: {user.username}")

# Create a client for authenticated requests
client = Client()
client.force_login(user)

try:
    # Get ListView
    url = reverse('kutub:manuscript-list')
    response = client.get(url)
    if response.status_code != 200:
        print(f"Error: Got status code {response.status_code} for manuscript list")
    else:
        # Save the rendered content
        file_path = f"{output_dir}/manuscript_list.html"
        html_content = process_html(response.content.decode('utf-8'))
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Exported: manuscript_list.html")        

    # Process each manuscript    
    for manuscript in Manuscript.objects.all():
        try:
            # Get the detail URL for this manuscript
            url = reverse('kutub:manuscript-detail', kwargs={'slug': manuscript.identifier})
            
            # Make a request through the client
            response = client.get(url)
            
            if response.status_code == 200:
                # Save the rendered content
                file_path = f"{output_dir}/{manuscript.identifier}.html"
                html_content = process_html(response.content.decode('utf-8'))
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"Exported: {manuscript.pk}_{manuscript.slug}.html")
                iiif_url = reverse('kutub:manuscript-iiif', kwargs={'slug': manuscript.slug})
                iiif_response = client.get(iiif_url)
                if iiif_response.status_code == 200:
                    iiif_path = f"{output_dir}/manuscripts/iiif/{manuscript.identifier}.html"
                    os.makedirs(os.path.dirname(iiif_path), exist_ok=True)
                    with open(iiif_path, "w", encoding="utf-8") as f:
                        f.write(iiif_response.content.decode('utf-8'))
                    print(f"Exported IIIF viewer: {manuscript.identifier}")
            else:
                print(f"Error: Got status code {response.status_code} for manuscript {manuscript.identifier}")
        
        except Exception as e:
            print(f"Error exporting manuscript {manuscript.pk}: {str(e)}")
            import traceback
            traceback.print_exc()
finally:
    # Restore original ALLOWED_HOSTS
    settings.ALLOWED_HOSTS = original_allowed_hosts

print(f"All manuscripts exported to {output_dir}")