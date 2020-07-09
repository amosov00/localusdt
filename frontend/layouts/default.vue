<template>
  <div>
    <Navbar />
    <div class="container">
      <nuxt />
    </div>
    <Footer />
  </div>
</template>

<script>
import Navbar from "~/components/Navbar";
import Footer from "~/components/Footer";
export default {
  components: { Navbar, Footer },
  middleware: ["fetchUser"]
};
</script>

<style scoped></style>
