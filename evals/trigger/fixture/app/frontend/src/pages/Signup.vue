<template>
  <form @submit.prevent="submit">
    <input v-model="email" /><input v-model="password" type="password" />
    <button type="button" @click="checkEmail">Check email</button>
    <button type="submit">Sign up</button>
  </form>
</template>
<script>
import { api } from "../api";
export default {
  data: () => ({ email: "", password: "" }),
  methods: {
    async checkEmail() { await api.get("/users/exists", { params: { email: this.email } }); },
    async submit() { const r = await api.post("/auth/signup", { email: this.email, password: this.password }); localStorage.token = r.data.token; this.$router.push("/cart"); },
  },
};
</script>
