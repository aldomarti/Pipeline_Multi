import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';

import { WebComponentRoutingModule } from '@web-component/web-component-routing.module';
import { HomePageComponent } from '@web-component/theme/pages/home-page/home-page.component';

@NgModule({
  declarations: [HomePageComponent],
  imports: [CommonModule, WebComponentRoutingModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class WebComponentModule {}
