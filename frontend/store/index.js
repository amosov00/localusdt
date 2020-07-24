import _ from "lodash";

export const state = () => ({
	user: null,
});

export const getters = {
	user: s => s.user,
};

export const mutations = {
	setUser: (state, user) => (state.user = user),
	deleteUser: state => (state.user = null),
};

export const actions = {
	async signUp({ commit }, data) {
		if (!data) return false;
		return await this.$axios
			.post("/account/signup/", {
				email: data.email,
				password: data.password,
			})
			.then(resp => {
				this.$axios.setToken(resp.data.token, "Bearer");
				this.$cookies.set("token", resp.data.token, {
					path: "/",
					maxAge: 60 * 60 * 24 * 7
						});
				commit("setUser", resp.data.user);
				this.$toast.showMessage({ content: 'Вы успешно зарегистрировались!' })
				return this.$router.push({ path: '/' })
			})
			.catch(_ => {
			});
	},
	async logIn({ commit }, data) {
		return await this.$axios
			.post("/account/login/", {
				email: data.email,
				username: data.userName,
				password: data.password,
				repeat_password: data.passwordRepeat,
			})
			.then(resp => {
				this.$axios.setToken(resp.data.token, "Bearer");
				this.$cookies.set("token", resp.data.token, {
					path: "/",
					maxAge: 60 * 60 * 24 * 7
				});
				commit("setUser", resp.data.user);
				this.$toast.showMessage({ content: 'Успешный вход в систему!' })
				return this.$router.push({ path: '/' })
			})
			.catch(_ => {
			});
	},
	logOut({commit}) {
		commit('deleteUser');
		this.$axios.setToken(null);
		this.$cookies.remove('token');
		this.$router.push('/')
	},
	async changeProfile({}, data) {
		return await this.$axios.put("/account/user/", data)
			.then(_ => {
				return true;
			})
			.catch(err => {
				return false;
			});
	},
	async changePassword({}, data) {
		return await this.$axios.post("/account/change_password/", data)
			.then(_ => {
				this.$toast.showMessage({ content: 'Пароль изменен!' })
				this.$router.push('/profile')
				return true;
			})
			.catch(err => {
				return false;
			});
	},
	async activateAccount({}, data) {
		if (!data) return false;
		return await this.$axios
			.post("/account/verify/", data)
			.then(resp => {
				return resp.data;
			})
			.catch(_ => {
				return false;
			});
	},

};
