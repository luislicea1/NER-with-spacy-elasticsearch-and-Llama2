import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import global_en from "./components/translation/en/global.json"
import global_es from "./components/translation/es/global.json"
import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';
import { I18nextProvider } from 'react-i18next';

i18next
 .use(initReactI18next) 
 .init({
    debug: true, 
    interpolation: { escapeValue: false },
    lng: "en",
    resources: {
      en: {
        global: global_en
      },
      es: {
        global: global_es
      },
    },
 });

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <I18nextProvider i18next = {i18next}>
      <App />
    </I18nextProvider>
  </React.StrictMode>,
)
