import Vue from 'vue'
import VueRouter from 'vue-router'
import UserHome from '@/components/UserHome';
import Welcome from '@/components/Welcome';
import MainPage from '@/components/MainPage';
import Dialogue from '@/components/Dialogue';
import Create from '@/components/Create';
import CreateRole from '@/components/CreateRole';
import Login from '@/components/Login';
import Report from '@/components/Report';
import GenerateAvatar from '@/components/GenerateAvatar';
import AccountManagement from '@/components/AccountManagement';
import CharacterManagement from '@/components/CharacterManagement';
import TestUpload from '@/components/TestUpload';
Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  {
    path: '/userhome',
    component: UserHome,
    redirect: '/mainpage',
    children: [
      { path: '/welcome', component: Welcome },
      { path: '/mainpage', component: MainPage },
      { path: '/dialogue', component: Dialogue },
      { path: '/createrole', component: CreateRole },
      { path: '/report', component: Report },
      { path: '/accountmanagement', component: AccountManagement },
      { path: '/charactermanagement', component: CharacterManagement },
      { path: '/test', component: TestUpload }
    ]
  },
]

const router = new VueRouter({
  routes
})

export default router
