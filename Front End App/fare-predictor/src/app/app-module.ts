import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing-module';
import { App } from './app';

import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Predictorcomponent } from './predictorcomponent/predictorcomponent';


@NgModule({
  declarations: [
    App,
    Predictorcomponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
   // Predictor
  ],
  providers: [
    provideBrowserGlobalErrorListeners()
  ],
  bootstrap: [App]
})
export class AppModule { }
