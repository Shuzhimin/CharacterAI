import Vue from 'vue'
import VueRouter from 'vue-router'
import UserHome from '@/components/UserHome';
import Welcome from '@/components/Welcome';
import MainPage from '@/components/MainPage';
import Dialogue from '@/components/Dialogue';
import Create from '@/components/Create';
import CreateRole from '@/components/CreateRole';
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: UserHome,
    redirect: '/mainpage',
    children: [
      { path: '/welcome', component: Welcome },
      { path: '/mainpage', component: MainPage },
      { path: '/dialogue', component: Dialogue },
      { path: '/createrole', component: CreateRole }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
