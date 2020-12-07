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
    async getInvoices({commit}, payload = 'not_active'){
        let result =  await this.$axios.get(`/admin/invoices/${payload}/`)
        let res = result.data.map(async e => {
            let buyer =  await this.$axios.get(`/admin/users/info/${e.buyer_id}`)
            e.buyer_id = buyer.data.username
            return e
        });
         Promise.all(res).then(function(e) {
            commit('getInvoices', e)
            return e
        })
    },
    async getUsers({commit}){
        let result =  await this.$axios.get(`/admin/users/`)
        console.log(result.data);
        commit('getUsers', result.data)
    }
}
