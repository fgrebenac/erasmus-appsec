package com.anteifilip.appsec.ui

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.anteifilip.appsec.models.Post
import com.anteifilip.appsec.models.PostBody
import com.anteifilip.appsec.models.UserBody
import com.anteifilip.appsec.network.AppSecRepository
import kotlinx.coroutines.launch

class AppSecViewModel(private val repository: AppSecRepository) : ViewModel() {

    val loginResponse = MutableLiveData<String>()
    val loginError = MutableLiveData<Unit>()

    val userResponse = MutableLiveData<Unit>()
    val userError = MutableLiveData<Unit>()

    val postResponse = MutableLiveData<Unit>()
    val postError = MutableLiveData<Unit>()

    val getPostsResponse = MutableLiveData<List<Post>>()
    val getPostsError = MutableLiveData<Unit>()

    val deletePostResponse = MutableLiveData<Unit>()
    val deletePostError = MutableLiveData<Unit>()

    val getPostResponse = MutableLiveData<Post>()
    val getPostError = MutableLiveData<Unit>()

    fun login(userBody: UserBody) = viewModelScope.launch {
        val response = repository.login(userBody)
        if (response.isSuccessful) loginResponse.value = response.body()
        else loginError.value = Unit
    }

    fun user(userBody: UserBody) = viewModelScope.launch {
        val response = repository.user(userBody)
        if (response.isSuccessful) userResponse.value = response.body()
        else userError.value = Unit
    }

    fun post(userId: String, post: PostBody) = viewModelScope.launch {
        val response = repository.post(userId, post)
        if (response.isSuccessful) postResponse.value = response.body()
        else postError.value = Unit
    }

    fun getPosts(userId: String) = viewModelScope.launch {
        val response = repository.getPosts(userId)
        if (response.isSuccessful) getPostsResponse.value = response.body()
        else getPostsError.value = Unit
    }

    fun deletePost(userId: String, postId: String) = viewModelScope.launch {
        val response = repository.deletePost(userId, postId)
        if (response.isSuccessful) deletePostResponse.value = response.body()
        else deletePostError.value = Unit
    }

    fun getPost(userId: String, postId: String) = viewModelScope.launch {
        val response = repository.getPost(userId, postId)
        if (response.isSuccessful) getPostResponse.value = response.body()
        else getPostError.value = Unit
    }

}