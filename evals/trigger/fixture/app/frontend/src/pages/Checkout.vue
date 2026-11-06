<template><div><button @click="pay">Pay</button><button @click="cancel">Cancel order</button></div></template>
<script>
import { api } from "../api";
export default {
  props: ["orderId"],
  async mounted() { this.cart = (await api.get("/cart")).data; },
  methods: {
    async pay() { const o = await api.post("/orders", { items: this.cart.items }); await api.post(`/orders/${o.data.id}/confirm`); },
    async cancel() { await api.post(`/orders/${this.orderId}/cancel`); },
  },
};
</script>
