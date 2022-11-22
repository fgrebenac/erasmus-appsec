package com.anteifilip.appsec.ui

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.anteifilip.appsec.R
import com.anteifilip.appsec.databinding.FragmentOnboardingBinding
import com.anteifilip.appsec.utils.onClickDebounced
import com.anteifilip.appsec.utils.viewBinding

class OnboardingFragment : Fragment(R.layout.fragment_onboarding) {

    private val binding by viewBinding(FragmentOnboardingBinding::bind)

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding.loginButton.onClickDebounced {
            findNavController().navigate(OnboardingFragmentDirections.openLogin())
        }
        binding.registerButton.onClickDebounced {
            findNavController().navigate(OnboardingFragmentDirections.openRegistration())
        }
    }

}