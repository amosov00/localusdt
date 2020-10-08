export default async function ({store, redirect}) {
  let user = store.state.user;

  if (user) {
    redirect('/')
  }
};
