<template>
  <div>
    <NotificationGroup />
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
import Toast from '~/components/app/Toast';
import NotificationGroup from "~/components/app/NotificationGroup";

export default {
  name: 'default-layout',
  components: { Navbar, Footer, Toast, NotificationGroup },
  middleware: ["fetchUser"]
};
</script>

<style></style>
