package com.anteifilip.appsec

import android.app.Application
import com.anteifilip.appsec.di.networkModule
import com.anteifilip.appsec.di.repositoryModule
import com.anteifilip.appsec.di.viewModelModule
import org.koin.android.ext.koin.androidContext
import org.koin.android.ext.koin.androidLogger
import org.koin.core.context.startKoin

class AppSecApplication : Application() {

    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidLogger()
            androidContext(this@AppSecApplication)
            modules(
                networkModule, repositoryModule, viewModelModule
            )
        }
    }
}