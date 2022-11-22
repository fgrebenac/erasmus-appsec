package com.anteifilip.appsec.di

import android.content.Context
import com.anteifilip.appsec.network.AppSecApiService
import com.anteifilip.appsec.network.AppSecRepository
import com.anteifilip.appsec.ui.AppSecViewModel
import com.anteifilip.appsec.utils.AuthInterceptor
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import org.koin.android.ext.koin.androidContext
import org.koin.dsl.module
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

val viewModelModule = module {
    factory { AppSecViewModel(get()) }
}

val repositoryModule = module {
    single { AppSecRepository(get()) }
}

val networkModule = module {
    factory { provideAppSecApi(get()) }
    factory { provideOkHttpClient(androidContext()) }
    single { provideRetrofit(get()) }
}

fun provideAppSecApi(retrofit: Retrofit): AppSecApiService =
    retrofit.create(AppSecApiService::class.java)

fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
    return Retrofit.Builder().baseUrl("http://10.0.2.2:5000/").client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create()).build()
}

fun provideOkHttpClient(context: Context): OkHttpClient {
    val loggingInterceptor = HttpLoggingInterceptor()
    loggingInterceptor.level = HttpLoggingInterceptor.Level.BODY
    return OkHttpClient().newBuilder().addInterceptor(loggingInterceptor)
        .addInterceptor(AuthInterceptor(context)).build()
}