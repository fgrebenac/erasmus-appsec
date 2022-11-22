package com.anteifilip.appsec.models

import java.io.Serializable

data class UserResponse(val id: String, val jwt: String) : Serializable