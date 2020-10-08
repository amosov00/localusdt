export default function ({route, redirect}) {
  const {path, query} = route
  console.log(route)
  if(path === '/ref' && query.id) {
    redirect('/signup?ref='+query.id)
  }
};
