export default function ({route, redirect}) {
  const {path, query} = route
  if(path === '/ref' && query.id) {
    redirect('/signup?ref='+query.id)
  }
};
