package com.anteifilip.appsec.ui

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.appcompat.app.AppCompatActivity
import com.anteifilip.appsec.R
import com.anteifilip.appsec.databinding.ActivitySplashBinding
import com.anteifilip.appsec.utils.PreferenceHelper
import com.anteifilip.appsec.utils.PreferenceHelper.get
import com.anteifilip.appsec.utils.viewBinding
import org.koin.androidx.viewmodel.ext.android.viewModel

@SuppressLint("CustomSplashScreen")
class SplashActivity : AppCompatActivity() {

    private val binding by viewBinding(ActivitySplashBinding::inflate)
    private val viewModel: AppSecViewModel by viewModel()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
        observeViewModel()
        checkAuthState()
    }

    private fun observeViewModel() {
        viewModel.isTokenValid.observe(this) { isValid ->
            if (isValid) startMain()
            else startOnboarding()
        }
    }

    private fun checkAuthState() {
        val token = PreferenceHelper.defaultPrefs(this).getString("token", null)
        token?.let {
            val userId = PreferenceHelper.defaultPrefs(this)["userId", ""]
            viewModel.checkAuthState(userId)
        } ?: run {
            startOnboarding()
        }
    }

    private fun startOnboarding() {
        Handler(Looper.getMainLooper()).postDelayed({
            val intent = Intent(this, OnboardingActivity::class.java)
            startActivity(intent)
            overridePendingTransition(
                R.anim.enter_from_right_anim,
                R.anim.exit_to_left_anim
            )
            finish()
        }, 500)
    }

    private fun startMain() {
        Handler(Looper.getMainLooper()).postDelayed({
            val intent = Intent(this, PostsActivity::class.java)
            startActivity(intent)
            overridePendingTransition(
                R.anim.enter_from_right_anim,
                R.anim.exit_to_left_anim
            )
            finish()
        }, 500)
    }
}