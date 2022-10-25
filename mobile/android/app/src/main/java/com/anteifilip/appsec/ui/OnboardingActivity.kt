package com.anteifilip.appsec.ui

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.anteifilip.appsec.databinding.ActivityOnboardingBinding
import com.anteifilip.appsec.utils.viewBinding

class OnboardingActivity : AppCompatActivity() {

    private val binding by viewBinding(ActivityOnboardingBinding::inflate)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
    }

}