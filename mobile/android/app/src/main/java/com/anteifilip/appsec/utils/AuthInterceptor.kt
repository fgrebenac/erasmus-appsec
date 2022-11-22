package com.anteifilip.appsec.utils

import android.content.Context
import okhttp3.Interceptor
import okhttp3.Response

class AuthInterceptor(private val context: Context) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val requestBuilder = chain.request().newBuilder()
        val token = PreferenceHelper.defaultPrefs(context).getString("token", null)
        token?.let {
            requestBuilder.addHeader("Authorization", "Basic $it")
        }
        return chain.proceed(requestBuilder.build())
    }
}