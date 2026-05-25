import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';

import { BlogRoutingModule } from '@blog/blog-routing.module';

import { HomePageComponent } from '@blog/theme/pages/home-page/home-page.component';
import { AboutPageComponent } from '@blog/theme/pages/about-page/about-page.component';

import { PostService } from '@blog/services/post-service/post-service';

@NgModule({ declarations: [HomePageComponent, AboutPageComponent], imports: [CommonModule, BlogRoutingModule], providers: [PostService, provideHttpClient(withInterceptorsFromDi())] })
export class BlogModule {}
