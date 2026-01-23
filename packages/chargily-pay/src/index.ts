export class ChargilyClient {
    constructor() {
        console.log("Chargily Client Initialized");
    }

    async createPayment() {
        return { checkout_url: "https://chargily.com/test/checkout" };
    }
}
