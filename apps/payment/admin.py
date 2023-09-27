# from django.contrib import admin
# from django.utils.safestring import mark_safe
#
# from apps.payment.models import (
#     InstallmentLog,
#     PaymentMerchantRequestLog,
#     Transaction,
#     TransactionStatus,
# )
#
#
# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ("id", "order", "transaction_id", "amount", "colored_status", "paid_at", "cancel_time")
#     list_display_links = ("id", "order")
#     list_filter = ("status",)
#     search_fields = (
#         "id",
#         "order__id",
#         "transaction_id",
#         "amount",
#         "paid_at",
#         "cancel_time",
#         "order__user__full_name",
#         "order__user__phone",
#     )
#
#     def colored_status(self, obj):
#         colors = {
#             TransactionStatus.WAITING: "gray",
#             TransactionStatus.PAID: "green",
#             TransactionStatus.FAILED: "red",
#             TransactionStatus.CANCELED: "black",
#         }
#         if obj.status:
#             return mark_safe(f'<span style="color:{colors[obj.status]}"><b>{obj.get_status_display()}</b></span>')
#         return f"{obj.status} --- null"
#
#     colored_status.short_description = "Status"  # type: ignore
#
#
# @admin.register(PaymentMerchantRequestLog)
# class PaymentMerchantRequestLogAdmin(admin.ModelAdmin):
#     list_display = ["id", "type", "response_status_code", "created"]
#     search_fields = ["id", "body", "header", "response", "method"]
#
#
# @admin.register(InstallmentLog)
# class InstallmentLogAdmin(admin.ModelAdmin):
#     list_display = ["id", "order", "transaction", "status", "created"]
#     search_fields = [
#         "id",
#         "order__user__full_name",
#         "order__user__phone",
#         "order__user__email",
#         "order__user__username",
#     ]
#     list_filter = ["status"]
