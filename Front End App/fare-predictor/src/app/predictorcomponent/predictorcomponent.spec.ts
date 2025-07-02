import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Predictorcomponent } from './predictorcomponent';

describe('Predictorcomponent', () => {
  let component: Predictorcomponent;
  let fixture: ComponentFixture<Predictorcomponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [Predictorcomponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Predictorcomponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
