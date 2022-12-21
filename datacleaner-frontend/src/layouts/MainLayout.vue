<template>
  <q-layout view="hHh lpR fFf">
    <q-header
      elevated
      class="q-pl-xl bg-primary text-white"
    >
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img
              inset-shadow
              src="https://images.pexels.com/photos/3977512/pexels-photo-3977512.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            >
          </q-avatar>
          Data cleaner
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer
      elevated
      class="primary text-white"
    >
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          <span> OpenU 2022</span>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>
