<template>
  <div>
    <Navbar />
    <Toast />
    <div class="container">
      <nuxt />
    </div>
    <Footer />
  </div>
</template>

<script>
import Navbar from "~/components/Navbar";
import Footer from "~/components/Footer";
import Toast from '~/components/app/Toast'
export default {
  name: 'default-layout',
  components: { Navbar, Footer, Toast },
  middleware: ["fetchUser"]
};
</script>

<style></style>
