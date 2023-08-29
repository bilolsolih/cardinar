from django.urls import path

from .api_endpoints import card, click, order, paylov, payme, uzum_bank

app_name = "payment"

urlpatterns = [
    # create course order
    path("CourseOrderCreate", order.CourseOrderCreateAPIView.as_view(), name="course-order-create"),
    # create video lesson order
    path("VideoLessonOrderCreate", order.VideoLessonOrderCreateAPIView.as_view(), name="VideoLessonOrderCreate"),
    # create webinar order
    path("WebinarOrderCreate", order.WebinarOrderCreateAPIView.as_view(), name="WebinarOrderCreate"),
    # get last transaction status
    path(
        "GetLastTransactionStatus/<int:order_id>",
        order.GetLastTransactionStatusAPIView.as_view(),
        name="get-last-transaction-status",
    ),
    # uzum bank info and pay apis
    path("ApelsinInfo", uzum_bank.ApelsinInfoAPIView.as_view(), name="apelsin-info"),
    path("ApelsinPay", uzum_bank.ApelsinPayAPIView.as_view(), name="apelsin-pay"),
    # payme
    path("Payme", payme.PaymeAPIView.as_view(), name="payme"),
    # click
    path("ClickPrepare", click.ClickPrepareAPIView.as_view(), name="click-prepare"),
    path("ClickComplete", click.ClickCompleteAPIView.as_view(), name="click-complete"),
    # karmon pay
    path("CreateUserCard", card.CreateUserCardAPIView.as_view(), name="create-user-card"),
    path("ConfirmUserCard", card.ConfirmUserCardAPIView.as_view(), name="confirm-user-card"),
    path("GetUserCardList", card.GetUserCardListAPIView.as_view(), name="get-user-card-list"),
    path("DeleteUserCard/<int:user_card_id>", card.DeleteUserCardAPIView.as_view(), name="delete-user-card"),
    # karmon pay callback
    path("Paylov", paylov.PaylovAPIView.as_view(), name="paylov"),
    # promo code
    path("CheckPromoCode/<str:code>", order.CheckPromoCodeAPIView.as_view(), name="check-promo-code"),
]
