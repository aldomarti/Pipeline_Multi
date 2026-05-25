import { Component, OnInit, ViewChild } from '@angular/core';

@Component({
  selector: 'home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent implements OnInit {
  @ViewChild('iframeElement') iframeElement: any;

  messageCanal: string = '';
  messages: String[] = [];

  onSubmit() {
    // SEND MESSAGE TO CHILD: Este código es para enviar el mensaje a la web hija: https://thankful-desert-0b23ed80f.3.azurestaticapps.net
    this.iframeElement.nativeElement.contentWindow.postMessage(
      `Desde canal: ${this.messageCanal}`,
      'https://thankful-desert-0b23ed80f.3.azurestaticapps.net'
    );
  }

  ngOnInit() {
    // LISTENING CHILD MESSAGE: Este código es para capturar mensaje de la web hija: https://thankful-desert-0b23ed80f.3.azurestaticapps.net
    window.addEventListener('message', (event) => {
      if (
        [
          'https://thankful-desert-0b23ed80f.3.azurestaticapps.net',
          'http://localhost:4200'
        ].includes(event.origin)) {
        this.messages.push(event.data);
      }
    });
  }
}
