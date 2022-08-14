import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils.translation import gettext, gettext_lazy


logger = logging.getLogger("util")


def get_limits(page, per_page, **kwargs):
    return slice((page - 1) * per_page, page * per_page, 1)


def get_pagination(page):
    return {
        "count": page.paginator.count,
        "total_pages": page.paginator.num_pages,
        "page": page.number,
        "per_page": page.paginator.per_page,
    }


def paginate(queryset, **kwargs):
    page = Paginator(queryset, kwargs["per_page"]).page(kwargs["page"])
    return {"list": page.object_list, "pagination": get_pagination(page)}


def localize(lang, default, ar=None, fr=None):
    if lang == "ar" and ar:
        return ar
    elif lang == "fr" and fr:
        return fr
    else:
        return default


def get_ctx_from_request(request):
    locale = request.headers.get("X-LOCALE") or f"{settings.LANGUAGE_CODE}-dz"
    language, country = (
        locale.split("-")[:2] if "-" in locale else (settings.LANGUAGE_CODE, "dz")
    )
    language = language if language in ("en", "ar", "fr") else settings.LANGUAGE_CODE
    country = country if country in ("dz",) else "dz"
    content = request.headers.get("x-content") or "desktop"

    if request.user.is_authenticated:
        user_id = request.user.id
        customer = vars(request.user).get(
            f"jobs_customer_profile"
        )  # FIXME {settings.PROJECT_NAME}
        customer_id = customer.pk if customer else None
        email = request.user.email
    else:
        email = None
        user_id = None
        customer_id = None

    return {
        "language": language,
        "country": country,
        "content": content,
        "user_id": user_id,
        "customer_id": customer_id,
        "email": email,
    }


def autocomplete_model(model, field, q, limit=50):
    from django.db.models import F

    filters = {f"{field}__icontains": q.strip()} if q else {}
    return (
        model.objects.filter(**filters)
        .order_by(field)[:limit]
        .values(key=F("id"), value=F(field))
    )


def filter_nones(l):
    return list(filter(lambda x: x, l))


def update_dict(d, u):
    import collections.abc

    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            if isinstance(v, list) and len(v) == 1:
                d[k] = v[0]
            else:
                d[k] = v
    return d


def localized_property(field_name):
    def get_localized_field(self):
        from context import ctx

        return (
            vars(self).get(f"{field_name}_{ctx.language}")
            or vars(self).get(f"{field_name}_en")
            or vars(self).get(f"{field_name}_fr")
            or vars(self).get(f"{field_name}_ar")
        )

    return property(get_localized_field)


def asset_url_property(field_name):
    def get_asset_url(self):
        try:

            field = getattr(self, field_name)

            return field and field.file and field.file.url
        except ObjectDoesNotExist:
            return None

    return property(get_asset_url)

