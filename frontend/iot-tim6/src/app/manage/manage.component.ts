// manage.component.ts

import { Component } from '@angular/core';

@Component({
  selector: 'app-manage',
  templateUrl: './manage.component.html',
  styleUrls: ['./manage.component.css']
})
export class ManageComponent {
  selectedColor: string = 'white';

  colorMappings: { [key: string]: boolean[] } = {
    'white': [true, true, true],
    'red': [true, false, false],
    'green': [false, true, false],
    'blue': [false, false, true],
    'yellow': [true, true, false],
    'purple': [true, false, true],
    'lightBlue': [false, true, true],
    'off': [false, false, false],
  };

  applyColor(): void {
    const rgbValues: boolean[] = this.colorMappings[this.selectedColor];
    
    console.log(`Applying RGB values: ${rgbValues}`);
  }
}
