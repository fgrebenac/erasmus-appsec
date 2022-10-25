package com.anteifilip.appsec.network

import com.anteifilip.appsec.models.Post
import com.anteifilip.appsec.models.PostBody
import com.anteifilip.appsec.models.UserBody
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.*

interface AppSecApiService {

    @POST("login")
    suspend fun login(@Body user: UserBody): Response<String>

    @POST("user")
    suspend fun user(@Body user: UserBody): Response<Unit>

    @POST("user/{userId}/post")
    suspend fun post(@Path("userId") userId: String, @Body post: PostBody): Response<Unit>

    @GET("user/{userId}/post")
    suspend fun getPosts(@Path("userId") userId: String): Response<List<Post>>

    @DELETE("user/{userId}/post/{postId}")
    suspend fun deletePost(
        @Path("userId") userId: String,
        @Path("postId") postId: String
    ): Response<Unit>

    @GET("user/{userId}/post/{postId}")
    suspend fun getPost(
        @Path("userId") userId: String,
        @Path("postId") postId: String
    ): Response<Post>

}