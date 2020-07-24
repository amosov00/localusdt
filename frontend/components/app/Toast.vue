<template>
	<div class="toast" v-if="show">
		<h2 class="toast__title">{{message}}</h2>
	</div>
</template>

<script>
export default {
	data() {
		return {
      show: false,
      message: ''
		}
  },
  methods: {
    halfLife() {
      setTimeout(() => {
        this.show = false
      },2000)
    }
  },
	created () {
		this.$store.subscribe((mutation, state) => {
			if (mutation.type === 'toast/showMessage') {
				this.message = state.toast.content
				this.color = state.toast.color
        this.show = true
        this.halfLife()
			}

		})
	}
}
</script>

<style lang="scss">
.toast {
	background-color: $green;
	width: 100vw;
		height: 50px;
		display: flex;
		align-items: center;
		justify-content: center;

	&__title {
		font-style: normal;
		font-weight: normal;
		font-size: 16px;
		color: $white;
	}
}
</style>
