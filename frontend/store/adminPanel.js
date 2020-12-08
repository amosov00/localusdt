export const state = () => ({
    invoices:null,
    users:null,
})

export const getters = {
    getInvoices(state){
        return state.invoices
    },
    getUsers(state){
        return state.users
    }
}

export const mutations = {
    getInvoices(state, payload){
        state.invoices = payload
    },
    getUsers(state, payload){
        state.users = payload
    },
}

export const actions = {
    async getInvoices({commit}){
        let result =  await this.$axios.get(`/admin/invoices/`)
        console.log(result);
        commit('getInvoices', result.data)
    },
    async getUsers({commit}){
        let result =  await this.$axios.get(`/admin/users/`)
        console.log(result.data);
        commit('getUsers', result.data)
    },
    async userStatus(state, payload){
        let url;
        if(payload.value == 1){
            url = `/admin/users/activate/${payload.user}/`
        }
        if(payload.value == 2){
            url = `/admin/users/deactivate/${payload.user}/`
        }
        if(payload.value == 3){
            url = `/admin/users/ban/${payload.user}/`
        }
        await this.$axios.put(url)
    }
}
