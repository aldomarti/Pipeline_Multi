import { Component } from '@angular/core';

import { environment } from '@environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'dso-angular-swa-sample-web';
  obfuscatedValue = environment.obfuscatedValue;
  cloudEnv = environment.cloudEnv;
  releaseVersion = environment.releaseVersion;
  commitId = environment.commitId;
}
