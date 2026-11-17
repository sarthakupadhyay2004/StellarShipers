from django.http import JsonResponse
from django.views.decorators.http import require_safe

from .models import Product


def public_products():
    return Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')


def image_data(request, image):
    return {'url': request.build_absolute_uri(image.image.url), 'caption': image.caption}


def images_for(product):
    # Use the prefetched list and retain the catalog's configured gallery order.
    return [image for image in product.images.all() if image.image]


def summary_data(request, product, images):
    primary = next((image for image in images if image.is_primary), images[0] if images else None)
    return {
        'slug': product.slug,
        'name': product.name,
        'category': product.category.name if product.category else '',
        'tagline': product.tagline,
        'description': product.description,
        'raw_material': product.raw_material,
        'origin': product.harvest_origin,
        'moq': product.moq,
        'is_featured': product.is_featured,
        'image': image_data(request, primary) if primary else None,
    }


@require_safe
def product_list(request):
    return JsonResponse({
        'products': [summary_data(request, product, images_for(product)) for product in public_products()],
    })


@require_safe
def product_detail(request, slug):
    product = public_products().prefetch_related('documents').filter(slug=slug).first()
    if product is None:
        return JsonResponse({'detail': 'Product not found.'}, status=404)

    images = images_for(product)
    data = summary_data(request, product, images)
    data.update({
        'packaging': product.packaging_details,
        'hs_code': product.hs_code,
        'supplier_notes': product.supplier_notes,
        'specifications': product.formatted_specs,
        'applications': product.applications if isinstance(product.applications, list) else [],
        'gallery': [image_data(request, image) for image in images],
        'documents': [
            {
                'title': document.title,
                'type': document.get_doc_type_display(),
                'file_size': document.file_size,
                'url': request.build_absolute_uri(document.document_file.url),
            }
            for document in product.documents.all() if document.document_file
        ],
    })
    return JsonResponse(data)
