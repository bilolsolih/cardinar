from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.payment.models import (
    InstallmentLog,
    Order,
    PaymentMerchantRequestLog,
    PromoCode,
    Transaction,
    TransactionStatus,
    UsedPromoCode,
    UserCard,
)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "type", "payment_type", "provider", "is_paid", "is_canceled")
    list_display_links = ("id", "user")
    list_filter = ("type", "payment_type", "provider", "is_paid", "is_canceled")
    search_fields = (
        "id",
        "user__username",
        "user__email",
        "user__full_name",
        "user__phone",
        "total_amount",
        "webinar__title",
        "course__title",
        "video_lesson__title",
    )
    # readonly_fields = (
    #     "id",
    #     "user",
    #     "course",
    #     "webinar",
    #     "video_lesson",
    #     "total_amount",
    #     "type",
    #     "payment_type",
    #     "provider",
    #     "is_paid",
    #     "is_canceled",
    # )

    # if you want to create order for testing payment integration you can comment this lines
    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "transaction_id", "amount", "colored_status", "paid_at", "cancel_time")
    list_display_links = ("id", "order")
    list_filter = ("status",)
    search_fields = (
        "id",
        "order__id",
        "transaction_id",
        "amount",
        "paid_at",
        "cancel_time",
        "order__user__full_name",
        "order__user__phone",
    )

    # readonly_fields = ("id", "order", "transaction_id", "amount", "status", "paid_at", "cancel_time")

    def colored_status(self, obj):
        colors = {
            TransactionStatus.WAITING: "gray",
            TransactionStatus.PAID: "green",
            TransactionStatus.FAILED: "red",
            TransactionStatus.CANCELED: "black",
        }
        if obj.status:
            return mark_safe(f'<span style="color:{colors[obj.status]}"><b>{obj.get_status_display()}</b></span>')
        return f"{obj.status} --- null"

    colored_status.short_description = "Status"  # type: ignore

    # if you want to create transaction for testing payment integration you can comment this lines
    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


@admin.register(PaymentMerchantRequestLog)
class PaymentMerchantRequestLogAdmin(admin.ModelAdmin):
    list_display = ["id", "provider", "type", "response_status_code", "created_at"]
    search_fields = ["id", "body", "header", "response", "method"]
    list_filter = ["provider"]


@admin.register(InstallmentLog)
class InstallmentLogAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "transaction", "status", "created_at"]
    search_fields = [
        "id",
        "order__user__full_name",
        "order__user__phone",
        "order__user__email",
        "order__user__username",
    ]
    list_filter = ["status"]

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False


@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "card_number"]
    search_fields = ["id", "user__username", "user__email", "user__full_name", "user__phone", "card_number"]
    list_filter = ["user"]
    list_display_links = ["id", "user"]


class PromoCodeResource(resources.ModelResource):
    start_date = resources.Field(
        column_name="start_date",
        attribute="start_date",
        widget=resources.widgets.DateWidget(format="%Y-%m-%d"),
    )
    end_date = resources.Field(
        column_name="end_date",
        attribute="end_date",
        widget=resources.widgets.DateWidget(format="%Y-%m-%d"),
    )

    class Meta:
        model = PromoCode
        fields = ["id", "code", "percent", "start_date", "end_date", "course"]


@admin.register(PromoCode)
class PromoCodeAdmin(ImportExportModelAdmin):
    resource_classes = [PromoCodeResource]
    list_filter = ["course", "start_date", "end_date"]
    search_fields = ["id", "code", "percent", "course__title"]


@admin.register(UsedPromoCode)
class UsedPromoCodeAdmin(admin.ModelAdmin):
    search_fields = ["promo_code__code", "user__username", "user__email", "user__full_name", "user__phone"]
