import * as React from 'react';
import { RouterProvider } from 'react-router-dom'
import { router } from './router/router'


function App() {
  return (
    <>
      <RouterProvider router={router}>
      </RouterProvider>
    </>
  );
}

export default App
