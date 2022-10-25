package com.anteifilip.appsec.models

import java.io.Serializable

data class Post(val id: String, val title: String, val content: String) : Serializable
