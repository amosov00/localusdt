<template>
	<section class="activate">
		<h1 class="activate__title">Активация почты</h1> 
	</section>
</template>

<script>
export default {
	name: 'activate',
	data: () => ({
		query: {
			verification_code: '',
			email: ''
				},
		}),
		async created() {
			if(this.success) {
				this.$axios.setToken(this.res.token, 'Bearer');
				this.$cookies.set('token', this.res.token, {
					path: '/',
					maxAge: 60 * 60 * 24 * 7,
				});
				this.$toast.showMessage({ content: 'Вы успешно зарегистрированны!' })
				await this.$authFetchUser()
				this.$router.push('/')
			}
		},
		async asyncData({ query, store }) {
			let res = await store.dispatch('activateAccount', query);

      if(res) {
        return { success: true, res }
      } else {
        return { success: false }
      }

		}

}
</script>

<style lang="scss">
	.activate {
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
