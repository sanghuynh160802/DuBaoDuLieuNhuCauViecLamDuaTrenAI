import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import {jwtDecode} from 'jwt-decode';

const isAdmin = (to: any, from: any, next: any) => {
    // const roles: boolean = useAuthStore().getIsAdmin(); 
    const access_token  = localStorage.getItem("access_token") as string
    const decodedToken = jwtDecode(access_token) as { role: string };
    const roles = decodedToken.role;
    if (roles == "admin") {
      next(); 
    } else {
      next('/403'); 
    }
  };
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/mainjob",
    },
    {
      path: "/mainjob",
      component: () => import("@/views/mainjob/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/job-opportunity",
      component: () => import("@/views/job-forecasting/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/cv-management",
      component: () => import("@/views/cv-management/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/applicant-cv-management",
      component: () => import("@/views/cv-management/applicant-cv-management/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/skill-management",
      component: () => import("@/views/skills-management/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/post",
      component: () => import("@/views/job-management/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/saved-post",
      component: () => import("@/views/saved-post/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/job-forecasting",
      component: () => import("@/views/job-forecasting/jobchart/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/vieclam24h",
      component: () => import("@/views/job-crawling_vieclam24h/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/itviec",
      component: () => import("@/views/job-crawling_itviec/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/topdev",
      component: () => import("@/views/job-crawling_topdev/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/login",
      component: () => import("@/views/login/index.vue"),
    },
    {
      path: "/register",
      component: () => import("@/views/register/index.vue"),
    },
    {
      path: "/dashboard",
      component: () => import("@/views/dashboard/index.vue"),
      meta: {
        layout: "default",
      },
      //beforeEnter: isAdmin,
    },
    {
      path: "/mainjob/:id",
      name: "JobDetail",
      component: () => import("@/views/jobdetails/index.vue"),
      props: true,
    },
    {
      path: "/user",
      component: () => import("@/views/user/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/forgotpassword",
      component: () => import("@/views/forgotpassword/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
      path: "/resetpassword",
      component: () => import("@/views/resetpassword/index.vue"),
      meta: {
        layout: "default",
      },
    },
    {
        path: '/403',
        name: 'Error403',
        component: () => import('@/views/error/index.vue'),
        meta: {
          layout: 'default',
        },
      },
  ],
});

export default router;
