# TUNA Backend — Architecture

This backend follows the **[HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide)**.
The project optimizes for **maintainability and explicitness** so new contributors can read one file
and understand the full contract. When in doubt, prefer the explicit, boring option from the guide.

## Stack
- Django 6 + Django REST Framework, PostgreSQL, **uv** for deps, **ruff** (lint/format) + **pyright** (types).
- Auth: cookie JWT via `dj-rest-auth` (see `tuna/settings/`). Global default permission is `IsAuthenticated`.

## App layout
Each app under `apps/` is organized by responsibility — one concern per file:

```
apps/<domain>/
  models.py       # ORM models only
  selectors.py    # READS  — functions that fetch/query data
  services.py     # WRITES — functions that create/update/delete + business logic
  apis.py         # HTTP layer — thin APIView classes (see below)
  urls.py         # explicit path() per API
  admin.py        # Django admin registration
```

`selectors.py` / `services.py` are added only when the app has reads / writes. Business logic lives
in selectors and services — **never** in `apis.py` or in serializers.

## APIs (`apis.py`)
- One **plain `APIView`** subclass per operation. **No** ViewSets, **no** routers.
- Name: `<Domain><Action>Api` — e.g. `AthleteListApi`, `SiteContentDetailApi`, `DashboardStatsApi`.
- The API is **thin**: validate input → call a selector/service → serialize output → return `Response`.
- Set `permission_classes` **explicitly** on every API, even when it matches the global default, so the
  auth contract is visible at the endpoint (`[AllowAny]` for public, `[IsAuthenticated]` for private).

## Serializers — explicit, inline, never reused
- Define serializers as **nested inner classes** named `InputSerializer` / `OutputSerializer` inside the API.
- Inherit from plain **`serializers.Serializer`**, **NOT `ModelSerializer`**. Declare **every field explicitly**.
  This keeps the output contract in one place and stops it drifting when a model field is added/renamed.
- **Do not** reuse a serializer across APIs. Duplicate the few fields instead — it's cheaper than the
  coupling. For nesting, use DRF/`inline_serializer`.

## Reference implementation (copy these)
`apps/athletes/` (list), `apps/site_content/` (public detail), `apps/dashboard/` (aggregate) are the
canonical examples. Minimal shape:

```python
# apis.py
class AthleteListApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        university = serializers.CharField(source="university.name")

    def get(self, request: Request) -> Response:
        athletes = athlete_list()                       # selector
        data = self.OutputSerializer(athletes, many=True).data
        return Response(data)
```

## Filtering & pagination
List APIs validate query params with a nested `FilterSerializer`, pass them to a selector that
applies the filters, and wrap results with `get_paginated_response` (`apps/common/pagination.py`,
a `LimitOffsetPagination` envelope). `AthleteListApi` is the canonical example — front-end controls
page size via `?limit=&offset=` (capped by the API's `Pagination.max_limit`).

## Not yet adopted (add when needed)
- **django-filter**: filters are applied by hand in the selector for now (a couple of fields). Adopt
  `django-filter` if filtering grows complex.
