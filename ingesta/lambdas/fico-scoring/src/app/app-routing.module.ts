import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { MainLayoutComponent } from '@app/theme/layouts/main-layout/main-layout.component';
import { HomePageComponent } from '@app/theme/pages/home-page/home-page.component';

const routes: Routes = [
  {
    path: '',
    component: MainLayoutComponent,
    children: [
      {
        path: '',
        component: HomePageComponent,
      },
      {
        path: 'blog',
        loadChildren: () =>
          import(
            /* webpackChunkName: "blog-module" */
            'src/app/modules/blog/blog.module'
          ).then(
            (mod) => mod.BlogModule
          ),
      },
      {
        path: 'dashboard',
        loadChildren: () =>
          import(
            /* webpackChunkName: "dashboard-module" */
            'src/app/modules/dashboard/dashboard.module'
          ).then(
            (mod) => mod.DashboardModule
          ),
      },
      {
        path: 'web-component',
        loadChildren: () =>
          import(
            /* webpackChunkName: "web-component-module" */
            'src/app/modules/web-component/web-component.module'
          ).then(
            (mod) => mod.WebComponentModule
          ),
      },
      {
        path: 'iframe',
        loadChildren: () =>
          import(
            /* webpackChunkName: "iframe-module" */
            '@iframe/iframe.module'
          ).then((mod) => mod.IframeModule),
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
