const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Đường dẫn đến file proto (giống trong index.js)
const PROTO_PATH = path.join(__dirname, 'proto/demo.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

const protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
const paymentService = new protoDescriptor.hipstershop.PaymentService(
    'localhost:50051', // Gọi vào chính container
    grpc.credentials.createInsecure()
);

console.log('--- Đang gửi yêu cầu thanh toán thử nghiệm ---');

const request = {
    amount: {
        currency_code: 'USD',
        units: 100,
        nanos: 0
    },
    credit_card: {
        // Số thẻ Visa Test hợp lệ
        credit_card_number: '4111111111111111', 
        credit_card_cvv: '123',
        credit_card_expiration_year: 2030,
        credit_card_expiration_month: 12
    }
};
paymentService.Charge(request, (err, response) => {
    if (err) {
        console.error('❌ Lỗi:', err);
    } else {
        console.log('✅ Thanh toán thành công! Transaction ID:', response.transaction_id);
    }
});
