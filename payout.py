

def callback_task(wallet_action_id):
    client = get_superpay_client()
    wallet_action = WalletAction.get(wallet_action_id)
    with transaction.atomic():
        metadata = wallet_action.metadata
        result = client.payout(wallet_action.merchant_id, metadata['wallet_id'], wallet_action.summ)
        metadata['response'] = result
        wallet_action.status = WalletAction.status.processing
        wallet_actions.save()


class PayoutView(views.APIView):
    parser_classes = (FormParser,)
    serializer_class = PayOutSerializer
    success_code = status.HTTP_202_ACCEPTED

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        callback_task(request.user.id, data)
        return Response(
            data={},
            status=self.success_code,
            content_type='application/json',
        )


class SuperpayCallbackView(views.APIView):
    parser_classes = (FormParser,)
    serializer_class = SuperpayCallbackSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        callback_processor_task(data)
        return Response(
            data={'status': 'success'},
            status=self.success_code,
            content_type='application/json',
        )
