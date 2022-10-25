package com.anteifilip.appsec.network

import com.anteifilip.appsec.models.PostBody
import com.anteifilip.appsec.models.UserBody

class AppSecRepository(private val apiService: AppSecApiService) {

    suspend fun login(user: UserBody) = apiService.login(user)

    suspend fun user(user: UserBody) = apiService.user(user)

    suspend fun post(userId: String, post: PostBody) = apiService.post(userId, post)

    suspend fun getPosts(userId: String) = apiService.getPosts(userId)

    suspend fun deletePost(userId: String, postId: String) = apiService.deletePost(userId, postId)

    suspend fun getPost(userId: String, postId: String) = apiService.getPost(userId, postId)

}